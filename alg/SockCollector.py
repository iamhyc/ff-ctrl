
class SockCollector(object):
    self.sock.connect((svr_ip, SVR_PORT))
    pass

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        raise(e) #print(e)
    finally:
        exit()