import numpy
import zmq
import functools
import uuid
import cv2

def array_to_msg(nparray):
    """
    Convert a numpy ndarray to its multipart zeromq message representation.
    The return list is composed of:
      0. The string representation of the array element type, i.e. 'float32'
      1. The binary string representation of the shape of the array converted to a numpy array with dtype int32
      2. The binary string representation of the array
    These informations together can be used from the receiver code to recreate
    uniquely the original array.
    @param nparray: A numpy ndarray
    @type nparray: numpy.ndarray
    @rtype: list
    @return: [dtype, shape, array]
    """
    _shape = numpy.array(nparray.shape, dtype=numpy.int32)
    return [nparray.dtype.name.encode(),
            _shape.tobytes(),
            nparray.tobytes()]

def msg_to_array(msg):
    """
    reverse the array_to_message function in order to recover the proper
    serialization of the array.
    @param msg: the array representation in a list as serizlized by
                array_to_msg
    @return: the numpy array
    """
    _dtype_name = msg[0].decode()
    _shape = numpy.fromstring(msg[1], numpy.int32)
    _array = numpy.fromstring(msg[2], _dtype_name)
    return (_dtype_name, _shape, _array.reshape(tuple(_shape)))

def sender_msg_to_array(msg):
    """
    Parse a list argument as returned by L{array_to_msg} function of this
    module, and returns the numpy array contained in the message body.
    @param msg: a list as returned by L{array_to_msg} function
    @rtype: numpy.ndarray
    @return: The numpy array contained in the message
    """
    [_dtype, _shape, _bin_msg] = msg_to_array(msg[2:])
    _uuid = uuid.UUID(bytes=msg[0])
    _data_name = msg[1].decode()
    return (_uuid, _data_name, _dtype, _shape, _bin_msg)

def numpy_array_sender(name, endpoint, sender_id="", socket_type=zmq.PUSH):
    """
    Decorator Factory
    The decorated function will have to return a numpy array, while the
    decorator will create a zmq socket of the specified socket type connected
    to the specified endpoint.
    Each time the function is called the numpy array will be sent over the
    instantiated transport after being converted to a multipart message using
    L{array_to_msg} function. The multipart message is prepended with a UUID
    and the given name as the first two elements.
    #TODO: Would it be good to add the possibility of transimitting arbitrary
    metadata? --- Marco Bartolini 27/04/2012
    Usage example::
        import zmq
        import zmqnumpy
        import numpy
        @zmqnumpy.numpy_array_sender(\"mysender\", \"tcp://127.0.0.1:8765\")
        def random_array_generator(min, max, width):
            return numpy.random.randint(min, max, width)
    @type name: string
    @param name: the label of the data stream
    @type endpoint: string
    @param endpoint: a zmq endpoint made as \"protocol://host:port\"
    @param sender_id: sender identifier, if not given a uuid will be generated
    automatically
    @param socket_type: a zmq socket type such as zmq.PUSH or zmq.PUB
    """
    _context = zmq.Context.instance()
    _socket = _context.socket(socket_type)
    _socket.connect(endpoint)
    if not sender_id:
        _uuid = uuid.uuid4().bytes
    else:
        _uuid = sender_id
    def wrapper(fn):
        @functools.wraps(fn)
        def wrapped(*args, **kwargs):
            _data = fn(*args, **kwargs)
            print(len(array_to_msg(_data)[2]))
            _socket.send_multipart([_uuid, name.encode()] + array_to_msg(_data))
        return wrapped
    return wrapper



def send():
    cap_idx = input("Capture Device: ")
    cap = cv2.VideoCapture(int(cap_idx), cv2.CAP_AVFOUNDATION)
    if not (cap.isOpened()):
        print("could not open device")
        exit()

    @numpy_array_sender("mysender", "tcp://127.0.0.1:8765")
    def frameYielder():
        nonlocal cap
        ret, frame = cap.read()
        print(frame.shape)
        return frame
    for _ in range(1000):
        frameYielder()
        
    
    cap.release()
    
if __name__ == "__main__":
    send()